% order5v2_0661  eq1=9811 eq2=33855  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,Z),f(W,f(U,Y)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,X),f(X,f(Y,Z))),X) )).
