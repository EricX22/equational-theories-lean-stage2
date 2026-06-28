% hard3_0158  eq1=1332 eq2=1146  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,Z),X),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(Z,f(X,X)),X)) )).
