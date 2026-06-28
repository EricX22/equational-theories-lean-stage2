% hard3_0102  eq1=806 eq2=2868  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,W),X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,f(Y,X)),Z),X) )).
