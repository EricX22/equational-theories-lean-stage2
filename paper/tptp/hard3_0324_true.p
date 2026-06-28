% hard3_0324  eq1=3034 eq2=1228  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,W)),Z),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(f(X,Y),X),X)) )).
