% hard3_0270  eq1=2567 eq2=2849  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(Z,X),X)),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,f(X,X)),Y),X) )).
