% hard3_0273  eq1=2633 eq2=3670  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,W),W)),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(X,Y),f(Z,X)) )).
