% hard3_0206  eq1=1924 eq2=3338  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(Y,f(Y,X)),f(Y,X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(W,Y))) )).
