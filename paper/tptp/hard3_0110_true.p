% hard3_0110  eq1=885 eq2=2939  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(X,Y),f(Z,X))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(Y,f(Y,X)),Y),X) )).
