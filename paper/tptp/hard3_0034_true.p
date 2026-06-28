% hard3_0034  eq1=176 eq2=1096  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(Y,Y),f(X,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(X,f(Z,Y)),X)) )).
