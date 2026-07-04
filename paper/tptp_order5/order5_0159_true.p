% order5_0159  eq1=37841 eq2=19562  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,f(Z,Z))),Y),X) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,Z),f(f(W,W),f(U,Y))) )).
