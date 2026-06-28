% hard3_0010  eq1=49 eq2=3867  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(X,f(X,f(Y,X))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(X,f(Y,X)),X) )).
