% hard3_0019  eq1=78 eq2=1405  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Y,f(Z,X))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,W),Y),X)) )).
