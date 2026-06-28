% hard3_0124  eq1=1014 eq2=1577  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(U,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(Z,X))) )).
