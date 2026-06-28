% hard3_0061  eq1=404 eq2=3339  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(Z,Z),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(W,Z))) )).
