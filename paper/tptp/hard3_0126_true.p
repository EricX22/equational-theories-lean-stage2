% hard3_0126  eq1=1014 eq2=2480  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(U,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(f(Y,Z),Y)),X) )).
